import Hero from "@/components/Hero";
import Map from "@/components/Map";

export default function Home() {

  return (
    <div className="bg-beige justify center items-center">
      <div className="bg-darkbrown h-[6vh] w-full"/>
      <div className="bg-lightbrown h-[6vh] w-full"/>
      <Hero />
      {/* <Map /> */}
    </div>
  );
}
