// create a global store to hold and update both the state(data) and function
import { create } from "zustand"
// a tool that connects Zustand’s state to a developer tool
import { mountStoreDevtool } from "simple-zustand-devtools"

/*
useAuthStore: store user information
set: set or update the store
get: access to the store
*/
const useAuthStore = create((set, get) => ({
    allUserDate: null, //store detail when user is login
    loading: false,

    // to retrieve specific detail abour user
    user: () => ({
        user_id: get().allUserDate?.user_id || null, // ? if user_id did not exit it return null
        username: get().allUserDate?.username || null, // // ? if username did not exit it return null

    }),
    // update allUserData with new user information
    setUser: (user) => set({
        allUserDate: user,
    }),

    setLoading: (loading) => set({ loading }),

    isLoggedIn: () => get().allUserDate !== null,
}))

if (!import.meta.env.DEV) {
    mountStoreDevtool("store", useAuthStore)
}

export { useAuthStore };