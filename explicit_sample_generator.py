import sys
import numpy.random as rd

class CalculatorFunction:
    def __init__(self, function):
        self.function = function

    def calculate(self, variables):
        return self.function(variables)

def generate_variable(lower, upper):
    return lower + (upper - lower) * rd.random()

def pithagora(variables):
    a = variables[0]
    b = variables[1]
    return a*a + b*b

def generate_sample_line(sample_domain, sample_codomain):

    string = ' '.join([str(x) for x in sample_domain])
    string += " " + str(sample_codomain)
    return string

def filesave_domain_codomain(domain, codomain, filename):
    file = open(filename, 'w')
    size = len(domain)

    sample_size = len(domain)
    var_size = len(domain[0])
    file.write("{0} {1}\n".format(sample_size, var_size))

    for i in range(size):
        sample_domain = domain[i]
        sample_line = sample_domain
        if codomain is not None:
            sample_codomain = codomain[i]
            sample_line = generate_sample_line(sample_domain, sample_codomain)

        file.write(sample_line + "\n")

    file.close()

def sample_generator(nSamples, nVars, lower, upper, calculator):
    domain = []
    codomain = []

    function = CalculatorFunction(calculator)

    for i in range(0, nSamples):
        x = []
        for j in range(nVars):
            variable = generate_variable(lower, upper)
            x.append(variable)

        y = function.calculate(x)

        domain.append(x)
        codomain.append(y)

    return domain, codomain

if __name__ == '__main__':
    filename = sys.argv[1]
    nSamples = int(sys.argv[2])
    numberOfVars = int(sys.argv[3])
    lower = int(sys.argv[4])
    upper = int(sys.argv[5])

    domain, codomain = sample_generator(nSamples, numberOfVars, lower, upper, pithagora)
    filesave_domain_codomain(domain, codomain, filename)
