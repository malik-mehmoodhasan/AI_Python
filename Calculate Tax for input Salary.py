# Write a program that takes salary as input. Using conditional statements,
# calculate the final tax based on the following rules:
# • If the salary is less than 30,000 → Tax rate is 5%
# • If the salary is between 30,000 and 70,000 → Tax rate is 15%
# • If the salary is greater than 70,000 → Tax rate is 25%

# User input for salary
salary = float(input("Enter your salary: "))

# Calculate tax based on the given rules
if salary < 30000:
    tax_rate = 0.05
elif salary <= 70000:
    tax_rate = 0.15
else:
    tax_rate = 0.25

# Calculate the final tax amount
final_tax = salary * tax_rate

# Output the tax rate and the final tax amount
print("Tax rate:", tax_rate * 100, "%")
print("Tax amount:", final_tax)
