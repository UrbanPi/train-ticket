### Original fault description
> Industrial fault description:
> 
> The result of the Consumer Price Index (CPI) is wrong.
> There is a mistake in including the locked product in CPI calculation.
> 
> TrainTicket replicated fault description:
> 
> In our Train Ticket system, we replicate this fault in ticket price calculating.
> When calculating the second class seat price, the calculating process is wrong, leading to a fault.
> 
> 
> Fault replication:
> 
> Setup System:
> 
> 1. Use docker-compose to setup the TrainTicket system.
> 
> 
> Failure Triggering Usage Steps:
> 
> 1. Log in.
> 2. Click [Flow One].
> 3. Search for ticket from Shang Hai to Su Zhou, train type is High Speed Rail.
> 4. You will found the price of second class seat is much higher, leading to a fault.


### Notes
The correct way of calculating the ticket price is:

`price = distance * price_per_distance`

The factor `price_per_distance` can be configured by the application administrator. The comfort (first) and economy (second) 
class tickets have different factors ranging from 0.2 to 0.7 for economy and 1.0 for comfort in the default configuration. 
For one specific journey the factor for the comfort class is allways higher than the factor for the economy class, leading to
the assertion:

`comfort_class_price > economy_class_price`


In the faulty implementation prices are calculated as:

`economy_class_price = distance`
`comfort_class_price = distance * comfort_price_per_distance`

The values for `comfort_price_per_distance` in the faulty implementation range from 0.8 to 1.3 (see ts-price-service: InitData).

| Train Type             | Price Per Distance |
|------------------------|--------------------|
| GaoTieOne, GaoTieTwo   | 1.3                |
| DongCheOne             | 1.2                |
| ZhiDa, TeKuai, KuaiSu  | 0.8                |

For the suggested journey from Shanghai to Su Zhou there are only trains of type GaoTieOne and GaoTieTwo, which makes it 
difficult to spot the error without further domain knowledge, because the price of the comfort class ticket is still higher 
than the economy class ticket. In order to clearly see the failure one has to search for tickets from **Shang Hai -> Nan Jing**
or vice versa. There the assertion `comfort_class_price > economy_class_price` does not hold for the train type ZhiDa. 