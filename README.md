# Pi-and-Zappi
Pi A+ interfaced with MyEnergi Zappi via API
I wanted to make use of the spare energy generated by my solar PV installation.
So using the MyEnergi API and a Raspberry Pi I had spare (A+) I made this routine
When power generated exceeds that used by the house by 300W The system turns on a Sonoff socket
if the power is then higher still by 300W it turns on a second socket. I am sure this could be 
ported to many different plaatforms. It was useful to m and maybe useful to others. I used the sonoff
smart sokets flashed with Tomatsu. I used the sockets to turn on 500W heaters.
I realise there is a considerable amount of code optimisation that could be carried out
but for now this is working framework and gets to heats homes for low cost until I get a battery for the excess

I also ended up using a Pi Zero as the physical size meant I could house it in a smaller enclosure.

I added a cronjob that reboots the Pi every hour
