Background

The reason I decided to make this project was because I had 3 stepper motors lying around specifically the Keling Technology, Inc Hybrid Stepper Motor Type:KL23H276-30-4A. I would like to be able to use them and I recently got a power supply. I didn't really have any large constrainst for this project but I knew that I wanted to have the ability to add more motors later on as well as other peripherals that I might use in the future. I also wanted to under the guise of this project to make some simple cycloidal drives for the motors and see the extent of their strength. I later in the process decided it might be nice to attempt to turn this into a robotic arm because I find them cool, which in my opionion is a great reason. Also all parts should be purchased from Aliexpress, Lcsc, and Jlcpcb. I somehow forgot about the biggest constraint of all which is money, the goal is to keep it under $120 but if absolutely necessary could be stretched to $180 as I am making this for hackclub's outpost ysws.

Research

The first thing I wanted to reasearch was the motor drivers I was going to use. I took a look at aliexpress just searching up stepper motor drivers and saw three different options which went down to two when I realized for this big motor it probably needs a decently large stepper driver for the heat and other things. So I threw all the data about the motors into google and apparently it is quite close to being a nema 23 motor which I found slightly weird based on the size differences, but google probably knows better than me because its twice the size of a nema 17. So the two motor drivers I decided between was the TB6600 and the DM542. It was not very difficult to decide between the two as almost every source online unanimously says the DM542 is better.

I also took a look at many other different cnc controllers as I made the assumption that the board I am making is just a cnc controller without the logic and circuits for the spindle motor. I also was able to look at the controller boards for the large cnc machine and the small one that is in the shop at my school and other than the integrated psu and spindle motor stuff I had a good idea of what I needed to make to the board.

The microcontroller that I decided on was the esp32 s3 devkitc. Not only is this a decently powerful microcontroller, but it works with Arduino IDE which I found has integrated libraries for using stepper motors with the DM542. What was even better is I have two of these on hand so I could save some of my budget for other things. The esp32 also has integrated bluetooth and wifi capabilities so I could potentially make a webapp or something of the sort to connect to it and send commands to the motors, but the implementation for that will be later for now the goal is getting the motors to spin up.

Thinking about my 3d printer I decided an sd card is good to have because you never know when the need for the sd card could come up so some precautionary work is always good to have done.

I also wanted some optocouplers because I had seen them on some other boards and the purpose of them seems quite useful. They should mostly be electrically isolated from the rest of the board other than the 5v power which is fine so if something goes wrong and dumps a ton of voltage or current the optocoupler breaks or the 5v converter breaks and not the rest of the board. Thus allowing for safe addition of other inputs such as limit switches to not crash an axis if I'm doing something that has an axis, or probing a point in space.

Schematic



PCB

CAD

Checking

Future

BOM