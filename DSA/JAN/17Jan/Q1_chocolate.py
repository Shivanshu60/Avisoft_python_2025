def chocolates_from_wrappers(chocolates, wrappers):
    if wrappers < 2:
        return 0  
    new_chocolates = wrappers // 2
    remaining_wrappers = wrappers % 2

    # Recursively calculate chocolates from new wrappers
    return new_chocolates + chocolates_from_wrappers(new_chocolates, remaining_wrappers + new_chocolates)

def chocolates_in_a_day(money, chocolate_price):
    initial_chocolates = money // chocolate_price
    return initial_chocolates + chocolates_from_wrappers(initial_chocolates, initial_chocolates)

def chocolates_in_a_month(daily_money, chocolate_price, days_in_month):
    total_chocolates = 0
    for day in range(1, days_in_month + 1):
        # Skip alternate weekends (Saturdays and Sundays)
        if day % 7 == 6 or day % 7 == 0:  # Weekend
            continue
        total_chocolates += chocolates_in_a_day(daily_money, chocolate_price)
    return total_chocolates

# Data constraint given in question
DAILY_MONEY = 16 
CHOCOLATE_PRICE = 2  
DAYS_IN_MONTH = 30  

# Calculate total chocolates Raman can buy in a month
total_chocolates = chocolates_in_a_month(DAILY_MONEY, CHOCOLATE_PRICE, DAYS_IN_MONTH)

print(f"Raman can buy {total_chocolates} chocolates in a month.")
