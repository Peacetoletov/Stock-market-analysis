desired_rent = 30000
initial_deposit = 300000
monthly_deposit = 20000
cagr = 1.09         # 9% for small cap value 20% leverage (after inflation)
                    # (conservative)

cur_wealth = initial_deposit
yearly_deposit = monthly_deposit * 12
# required_wealth = desired_rent * 12 * 25      # 4% rule
required_wealth = desired_rent * 12 * 33.3      # 3% rule (safe)
years = 0
while cur_wealth < required_wealth:
    cur_wealth += yearly_deposit
    cur_wealth *= cagr
    years += 1

    print("After", years, "years, I have", round(cur_wealth), "CZK.")
