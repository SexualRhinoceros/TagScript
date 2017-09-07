import re, ast

from .exceptions import TagEngineError

REGEX = re.compile("[mM]{(.+[^}])}")

class MathEvaluationFilter():
    def Process(self, engine, text):
        value = text

        match = REGEX.search(value)
        if match is None:
            return value # Exit early if there is no math expressions to begin with

        while match is not None:
            for matched_group in match.groups():
                final_value = self.Process(self, engine, matched_group)
                try:
                    evaluation = ast.literal_eval(match.group(1))
                except Exception as e:
                    raise TagEngineError('{}: {}\nMATH EXPRESSION: {}'.format(type(e).__name__, str(e), match.group(1)))
                value = value.replace(match.group(0), str(evaluation))
                match = REGEX.search(value)

        return value
