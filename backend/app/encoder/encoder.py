import time

from rotary_irq_rp2 import RotaryIRQ



r = RotaryIRQ(pin_num_clk=20,

              pin_num_dt=21,

              min_val=0,

              reverse=True,

              pull_up=True,

              invert=False,

              range_mode=RotaryIRQ.RANGE_UNBOUNDED)



old_value = r.value()



while True:

    new_value = r.value()

    if new_value != old_value:

        old_value = new_value

        print(f'Value = {new_value}')

    time.sleep(0.5)

