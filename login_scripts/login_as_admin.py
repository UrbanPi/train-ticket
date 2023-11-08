from login import login_admin

if __name__ == '__main__':
    print("Returns the id of the admin and cookies from the login. The id seems to be used as a request parameter. \n"
          "The cookies do not seem to be that important. (Requests in the browser also work without the cookies as long as the id is correct)")
    print(login_admin(username="adminroot", password="adminroot"))
