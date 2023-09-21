"use client";

import {useEffect, useState} from "react";
import {redirect} from "next/navigation";


export default function Page() {
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    async function getUser() {
      const accessToken = localStorage.getItem("jwt")
      console.log(accessToken)
      if (accessToken) {
        setIsLoading(true)

        try {
          const response = await fetch(process.env.NEXT_PUBLIC_SERVER_ADDR + "/users/me", {
            headers: {
              "Authorization": `Bearer ${accessToken}`,
            }
          })
          if (response.status === 200) {
            const user = await response.json()
            console.log({user})
            localStorage.setItem("user", JSON.stringify(user))
          } else {
            localStorage.removeItem("user")
          }
        } catch (error) {
          console.error(error)
          localStorage.removeItem("user")
        } finally {
          setIsLoading(false)
        }
      }
    }

    getUser()
  }, []);

  async function onSubmit(event) {
    event.preventDefault()
    setIsSubmitting(true) // Set loading to true when the request starts

    try {
      const formData = new FormData(event.currentTarget)
      const response = await fetch(process.env.NEXT_PUBLIC_SERVER_ADDR + '/users/token', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      localStorage.setItem("jwt", data.access_token)

      const userResponse = await fetch(process.env.NEXT_PUBLIC_SERVER_ADDR + "/users/me", {
        headers: {
          "Authorization": "Bearer " + data.access_token,
        },
      })
      const userData = await userResponse.json()
      console.log({user: userData})
      localStorage.setItem("user", JSON.stringify(userData))
    } catch (error) {
      // Handle error if necessary
      console.error(error)
    } finally {
      setIsSubmitting(false) // Set loading to false when the request completes
    }
  }

  if (isLoading) {
    return (
        <div>
          <h1>Login</h1>
          <h2>Getting user data...</h2>
        </div>
    );
  } else {
    const user = localStorage.getItem("user")
    if (user) {
      redirect("/")
      return
    }

    return (
        <div>
          <h1>Login</h1>
          <form onSubmit={onSubmit}>
            <div>
              <label htmlFor="username">Username</label>
              <input id="username" name="username" type="text"/>
            </div>
            <div>
              <label htmlFor="password">Password</label>
              <input id="password" name="password" type="password"/>
            </div>

            <input type="submit" value={isSubmitting ? "Logging in..." : "Login"} disabled={isSubmitting}/>
          </form>
        </div>
    )
  }
}