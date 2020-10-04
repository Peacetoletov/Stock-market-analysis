desired_rent = 50000
initial_deposit = 300000
monthly_deposit = 20000
interest_rate = 1.11

cur_wealth = initial_deposit
yearly_deposit = monthly_deposit * 12
required_wealth = desired_rent * 12 * 25
years = 0
while cur_wealth < required_wealth:
    cur_wealth += yearly_deposit
    cur_wealth *= interest_rate
    years += 1

    print("After", years, "years, I have", round(cur_wealth), "CZK.")
