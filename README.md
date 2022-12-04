# GravitySim
Simulates Gravity using Python and Turtle, allowing you to add as many bodies as you want of whatever mass, size etc.

The Program runs of changes to a Dictionary called Body_Dict with the key being the name of the body, and the value being a Body Object. The bodies are iterated over, drawn to a canvas, and their gravitational influence is calculated upon eachother, which is saved to the Bodies instance variables, this then loops forever.

To Add a Body to the dictionary, use:
- Add_Body_Object: 
  Body_Dict = Add_Body_Object(mass, radius, position, color, velocity, InitialVelocity, Body_Dict, fixed, name)

![image](https://user-images.githubusercontent.com/103237702/205470523-e83fa8f8-bbf9-4d1d-8e06-e1d43f98e9ce.png)
