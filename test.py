from ndrive import ndrive
n = ndrive(debug=True)
n.login("carpedm20","nd3@dp03t")
n.uploadFile("README.md",'/test.md',True)
