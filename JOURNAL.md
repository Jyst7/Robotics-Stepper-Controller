**Background**

The reason I decided to make this project was for two reasons, the first being I wanted to justify procrastinating studying for exams and I'd feel bad if I was just doomscrolling and the second is because I had 3 stepper motors lying around specifically the Keling Technology, Inc Hybrid Stepper Motor Type:KL23H276-30-4A. I would like to be able to use them and I recently got a power supply. I didn't really have any large constrainst for this project but I knew that I wanted to have the ability to add more motors later on as well as other peripherals that I might use in the future. I also wanted to under the guise of this project to make some simple cycloidal drives for the motors and see the extent of their strength. I later in the process decided it might be nice to attempt to turn this into a robotic arm because I find them cool, which in my opionion is a great reason. Also all parts should be purchased from Aliexpress, Lcsc, and Jlcpcb. I somehow forgot about the biggest constraint of all which is money, the goal is to keep it under $120 but if absolutely necessary could be stretched to $180 as I am making this for hackclub's outpost ysws.

Research

The first thing I wanted to reasearch was the motor drivers I was going to use. I took a look at aliexpress just searching up stepper motor drivers and saw three different options which went down to two when I realized for this big motor it probably needs a decently large stepper driver for the heat and other things. So I threw all the data about the motors into google and apparently it is quite close to being a nema 23 motor which I found slightly weird based on the size differences, but google probably knows better than me because its twice the size of a nema 17. So the two motor drivers I decided between was the TB6600 and the DM542. It was not very difficult to decide between the two as almost every source online unanimously says the DM542 is better.

I also took a look at many other different cnc controllers as I made the assumption that the board I am making is just a cnc controller without the logic and circuits for the spindle motor. I also was able to look at the controller boards for the large cnc machine and the small one that is in the shop at my school and other than the integrated psu and spindle motor stuff I had a good idea of what I needed to make to the board.

The microcontroller that I decided on was the esp32 s3 devkitc. Not only is this a decently powerful microcontroller, but it works with Arduino IDE which I found has integrated libraries for using stepper motors with the DM542. What was even better is I have two of these on hand so I could save some of my budget for other things. The esp32 also has integrated bluetooth and wifi capabilities so I could potentially make a webapp or something of the sort to connect to it and send commands to the motors, but the implementation for that will be later for now the goal is getting the motors to spin up.

Thinking about my 3d printer I decided an sd card is good to have because you never know when the need for the sd card could come up so some precautionary work is always good to have done.

I also wanted some optocouplers because I had seen them on some other boards and the purpose of them seems quite useful. They should mostly be electrically isolated from the rest of the board other than the 5v power which is fine so if something goes wrong and dumps a ton of voltage or current the optocoupler breaks or the 5v converter breaks and not the rest of the board. Thus allowing for safe addition of other inputs such as limit switches to not crash an axis if I'm doing something that has an axis, or probing a point in space.

For the power situation I decided to underpower my motors a bit because my psu can safely go up to 32V which is I believe the reccomended amound for nema 23 motors I didn't really want to go near the top range of my PSU's capabilities so I thought 24V would work fine they just wouldn't be as powerful as they could be. This also made powering the pcb slightly easier as I already had a buck converter in mind. So I would take the 24V from the psu and buck it down to 5V which can power some things that are fine with a bit of noise and then I could use an LDO to get a clean 3.3v to the SD card and the esp32 which don't like a lot of noise.

Schematic

At this point in the project after all the research I had done I decided to just start doing the schematic. The first thing that I did was set up easyeda2kicad which is my savior for any kicad project because 90% of the lcsc parts I use have an easyeda footprint and schematic that can be ported over to kicad and it saves so much time that would be spent just making the symbols and footprints that 90% of the time I mess up when I make them custom. I threw in my parts starting with the esp32, the sd card, buck converter and ldo.

I started by putting together the buck converter and the ldo. These two components I have had lots of problems with in the past. So usually when I use them it ends up with the magic smoke being released from the devices and unfortunately you can't put that back in the component so I have often opted to just use a physical device that will give a stable 5v output and isolate the higher voltage, but this time I am pulling all the stops and found a popular buck converter that is specifically made with 12V and 24V in mind and following the schematic and reccomended component layout to a tee. Unfortunately for the LDO there is only a reccomended schematic so I followed that and I will have to figure out and get advice for the LDO part.

After this I threw up a bunch of screw terminals and immideately realized that the esp32 does not have enough pins for the optocouplers and 6 motors as each motor requires 3 pins to the motors PUL+ DIR+ and ENA+, ENA+ is slightly debatable because it could just be used for a software stop by pulling high, but if I really need to I can just cut power to the board, but if its an option might as well have it. So the only option rather than decide on a new microcontroller I just threw some shift registers on there and called it a day. I found that some shift registers I have used in the past will not work because it is recommended to use a specific one for this application. I don't remember the exact reason off the top of my head, but I think it was something about the communication being spi rather than i2c.

Then I threw together the optocouplers which I could not find any schematic advice or anything for so I found some other projects that used it, checked their use case and its implementation and then used their configuration and it should work for my use case as well.

PCB

I started routing the the buck converter according to the reccomended layout and I realized a bit late that two of the components had to be 1206 rather than the 0805 that I used so I had to redo the layout which was totally very fun. The LDO I kind of winged where I just routed overly large traces and added a bunch of ground vias, but from similar layouts for them that I have seen it should work.

Then I placed the rest of the footprints in the layout and organized them to the layout worked best and ajusted what gpios I would use. I had the screw terminals for the motors on one end, screw terminals for the optocouplers on the adjacent edge with the sd card and the power management on the top edge, with the esp32 on the left edge

With that done the rest of the wiring was simple, the only fancy-ish thing I added was decently large traces for the 5V and 3.3V.

Code

Code I will say is not my strongest suit, but I made a simple program that controls the motors. I started by using accelmotor which is a library that is used for controlling stepper motors through arduino ide. Unfortunately that does not work when using shift registers so I had to program it to work natively. With some research of the docs I found how to use the spi on the shift registers to then control the motors with the DIR+ and PUL+ pins. Then I just have it move backwards for a second and forwards for a second to test the motors.

The shift registers were extra interesting because three of them are daisy chained, and so I have to check which shift register the code connects to and then sends the proper output to the pin 1-7. The rest is pretty basic though for the main loop.

CAD

Checking

Future

BOM