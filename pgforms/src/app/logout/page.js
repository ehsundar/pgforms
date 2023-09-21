"use client"

import {redirect} from "next/navigation";

export default function Page() {
  localStorage.removeItem("user")
  localStorage.removeItem("jwt")
  redirect("/login")
}