print("Welcome to the daily calorie tracker")
meal_name=[]
calorie_amount=[]
a=input("Do you want to add a meal? (yes/no): ").lower()
while a=="yes":
    meal=input("Enter the meal name: ")
    calorie=int(input("Enter the calorie amount: "))
    meal_name.append(meal)
    calorie_amount.append(calorie)
    total_calories=sum(calorie_amount)
    a=input("Do you want to add another meal? (yes/no): ").lower()
avg_calories=total_calories/len(calorie_amount) 
daily_limit=int(input("Enter your daily calorie intake limit:"))
if total_calories>daily_limit:
    print("You have exceeded your daily calorie intake")
else:
    print("You are within your daily calorie intake")
for i in range(len(meal_name)):
    meal=f"{meal_name[i]}"
    print(meal)
for j in range(len(calorie_amount)):
    amt=f"{calorie_amount[j]}"
    print(amt)
print(total_calories)
print(avg_calories)
    