from pymorse import Morse

with Morse() as simu:

  motion = simu.mouse.motion

  while True:
      key = input("WASD?")

      if key.lower() == "w":
          print("w was hitttttttttttt")
          motion.properties(speed=4.0)
      else:
          continue

      motion.publish({"w": w})
