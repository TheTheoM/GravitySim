# GravitySim
Simulates Gravity using Python and Turtle, allowing you to add as many bodies as you want of whatever mass, size etc.

The Program runs of changes to a Dictionary called Body_Dict with the key being the name of the body, and the value being a Body Object. The bodies are iterated over, drawn to a canvas, and their gravitational influence is calculated upon eachother, which is saved to the Bodies instance variables, this then loops forever.

To Add a Body to the dictionary, use:
- Add_Body_Object: 
  Body_Dict = Add_Body_Object(mass, radius, position, color, velocity, InitialVelocity, Body_Dict, fixed, name)

![image](https://user-images.githubusercontent.com/103237702/205470556-2a76cfe8-6ee7-4878-aba1-4670769b41c8.png)
