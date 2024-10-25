class InstancePrices:
    def __init__(self, on_demand, up_all_upfront, up_partial_upfront, hr_partial_upfront, hr_no_upfront):
        self.on_demand = on_demand
        self.up_all_upfront = up_all_upfront
        self.up_partial_upfront = up_partial_upfront
        self.hr_partial_upfront = hr_partial_upfront
        self.hr_no_upfront = hr_no_upfront
    
    def get_effective_hourly_rate(market, res_duration):
        match market:
            case 'OnDemand':
                return self.on_demand
            case 'RAll':
                return self.up_all_upfront / res_duration
            case 'RPartial':
                return (self.up_partial_upfront / res_duration) + self.hr_partial_upfront
            case 'RNo':
                return self.hr_no_upfront