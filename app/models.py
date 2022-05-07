from django.db import models

class Global(models.Model):
    name = models.CharField(max_length=200)
    projection_period = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

VARIABLE_TYPES = [("Input","Input"), ("Table","Table"), ("Variable","Variable"),]
class Variable(models.Model):
    name = models.CharField(max_length=200)
    formula = models.TextField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    round = models.IntegerField(default=0)
    type = models.CharField(max_length=200, choices=VARIABLE_TYPES)

    def __str__(self):
        return self.name

    def values_round(self):
        rounding = self.round
        values = self.values()
        values_rounded = []
        for x in values:
            values_rounded.append(round(x,rounding))
        return values_rounded

    def values(self):
        values = []
        for t in range(10):
            values.append(self.value(t))
        return values

    def value(self, t):
        formula = self.formula.strip()
        formula = self.remove_if(formula, t).strip()
        formula = self.replace_variables(formula, t)
        formula = self.replace_t(formula, t)
        try:
            result = eval(formula)
        except:
            result = formula
        return result

    def replace_t(self, formula, t):
        if formula[0:5] == "Error": return formula
        formula = formula.replace("t", str(t))
        return formula

    def replace_variables(self, formula, t):
        for x in self.referenced_variables():
            start = formula.find(x.name)
            if start != -1:
                start_t = formula.find("(", start)
                end_t = formula.find(")", start)
                if start_t == -1 or end_t == -1:
                    return("Error - brackets not found")
                variable_str = formula[start:end_t+1]
                time_str = formula[start_t+1:end_t]
                time_str = time_str.replace("t", str(t))
                try:
                    t = eval(time_str)
                except:
                    return(f"Error - 'Time String' couldn't be evaluated: 'Time String': '{time_str}'")
                formula = formula.replace(variable_str, str(x.value(t)))
        return formula

    def remove_if(self, formula, t):
        found = formula.find("if")
        if found == -1:
            return formula
        else:
            # Get Logic Statement
            start = found + 2
            end = formula.find(":")
            logic_statement = formula[start:end]
            logic_statement_str = logic_statement.strip()
            logic_statement_str = self.replace_t(logic_statement_str, t)
            logic_statement_result = eval_logic(logic_statement_str)
            # Get True Statement
            start = end + 2
            end = formula.find("else")
            true_statement = formula[start:end].strip()
            # Get False Statement
            start = end + 5
            end = None
            false_statement = formula[start:end]
            if logic_statement_result:
                return true_statement
            else:
                return false_statement

    def referenced_variables(self):
        referenced_variables = []
        variables = Variable.objects.all()
        for y in variables:
            found = self.formula.find(y.name)
            if found != -1: referenced_variables.append(y)
        return referenced_variables

def eval_logic(formula):
    if formula == 'True': return True
    equals = formula.find("=")
    lhs = float(formula[0:equals])
    rhs = float(formula[equals+1:])
    return lhs == rhs