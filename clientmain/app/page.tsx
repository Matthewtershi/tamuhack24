import Footer from "@/components/Footer";
import Hero from "@/components/Hero";
import Map from "@/components/Map";
import { FloatingNav } from "@/components/ui/floatingNav";


export default function Home() {

  return (
    <div className="bg-beige justify center items-center">
      <FloatingNav navItems={[{ name: "Home", link: "#home" }, { name: "What We Do", link: "#map" },{ name: "Our Process", link: "#process"},]}/>
      <div className="bg-darkbrown h-[6vh] w-full"/>
      <div className="bg-lightbrown h-[6vh] w-full"/>
      <Hero />
      {/* <Map /> */}
      <Footer />
    </div>
  );
}
