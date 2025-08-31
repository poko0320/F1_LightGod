"use client";
import { Hero } from "@/components/hero/hero";
import { Footer } from "@/components/footer/footer";
import { Quote } from "@/components/quote/quote";
import { useRedirectWarning } from "@/lib/redirect";

export default function Home() {
  useRedirectWarning();

  return (
    <>
      <Hero />
      <Quote />
      <Footer />
    </>
  );
}
