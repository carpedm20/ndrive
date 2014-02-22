from ndrive import Ndrive
n = Ndrive(debug=True)
n.login("carpedm20","nd3@dp03t")
n.uploadFile("README.md",'/test.md',True)
