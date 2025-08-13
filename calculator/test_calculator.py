from pkg.calculator import Calculator

calc = Calculator()
result = calc.evaluate('3 + 7 * 2')
print(result)

if result == 17:
    print("Test passed!")
else:
    print("Test failed!")