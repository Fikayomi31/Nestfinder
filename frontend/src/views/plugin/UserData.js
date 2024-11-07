import Cookie from "js-cookie"
import jwtDecode from "jwt-decode"

/*
UserData: function access token and 
refresh token of user

*/

function UserData() {
    let access_token = Cookie.get("access_token")
    let refresh_token = Cookie.get("refresh_token")

    if (access_token && refresh_token) {
        const token = refresh_token
        const decode = jwtDecode(token)

        return decode
    } else {
        // pass
    }
}

export default UserData