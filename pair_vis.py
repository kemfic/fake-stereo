from OpenGL import GL as gl
import pangolin as pango
import cv2
import numpy as np

def main():
  pango.CreateWindowAndBind('fake stereo', 640, 480)

  # Projection and ModelView Matrices
  scam = pango.OpenGlRenderState(
                  pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 500, 100000),
                  pango.ModelViewLookAt(-10, -10, -10, 0, 0, 0, pango.AxisDirection.AxisY))
  handler = pango.Handler3D(scam)

  # Interactive View in Window
  disp_cam = pango.CreateDisplay()
  disp_cam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
  disp_cam.SetHandler(handler)
  w = 250
  h = 50
  img = cv2.imread('img/2.png')#[:w,70:500]
  disp = cv2.imread('img/out1.png',0) * 5.0#[:w,70:500] * 5.0
  print(disp[0,200])
  # Add point locations using pixel location and z-distance from disparity map
  # lazy man's point cloud
  mask = np.ones_like(disp) * 1.0
  #mask[disp < 5.0] = 0.0
  cv2.imshow('mask', mask*1000.0)
  grid = np.mgrid[0:img.shape[1], 0:img.shape[0]]
  grid = np.swapaxes(grid, 0,2)
  pts = np.dstack((grid,disp)) * 1.0
  pts[pts[:,:,-1] < 100.0] = [0,0,0]
  pts = -1.0 * pts.reshape(pts.shape[0]*pts.shape[1], 3)
  # Color matrix based on point location

  colors = img /512.0#np.dstack((img,img,img))
  colors = colors.reshape(colors.shape[0]*colors.shape[1],3)
  #colors[:, :] = 1. - img[:,:]/10
  #colors[:] = [0.5, 0.5, 0.5]
  while not pango.ShouldQuit():
    # Clear screen
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    #gl.glClearColor(0.15, 0.15, 0.15, 0.0)
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    disp_cam.Activate(scam)

    # Draw Points
    gl.glPointSize(3)
    gl.glColor3f(0.0, 1.0, 0.0)
    pango.DrawPoints(pts, colors)

    # Finish Drawing
    pango.FinishFrame()






if __name__ == '__main__':
  main()
