import matplotlib.pyplot as plt

# Values
years = [0,1,2,3]
years2 = [0,1,2,3]
initial_value = 33000
depreciation_rate = 0.12

# Calculate book values
book_values = [initial_value]
operation_values = [0,3400, 3900, 4400]
for year in range(1, len(years)):
    new_value = book_values[-1] * (1-depreciation_rate)
    book_values.append(new_value)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(years, book_values, marker='o')
plt.plot(years2, operation_values, marker='o')
plt.plot(years, [dep_value + op_value for dep_value, op_value in zip(book_values, operation_values)], marker='o')
plt.title('Economic Life EAC')
plt.xlabel('Year')
plt.ylabel('Book Value ($)')
plt.grid(True)
plt.legend()
plt.show()