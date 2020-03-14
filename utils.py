import cv2

def FrameCapture(video):

  count = 0
  success = 1
  images = []
  while success:
    success, image = video.read()
    try:
      images.append(image)
    except :
      print("That key does not exist!")

    count += 1
  print(len(images))
  return images

def makevideo(images, write_path, video_info):
  out = cv2.VideoWriter(write_path, 0x7634706d, 30, (images[0].shape[1], images[0].shape[0]))  # создаем видео
  for i in range(len(images)):
    out.write(images[i])  
  out.release()  
  cv2.destroyAllWindows()
  