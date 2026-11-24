import React, {useState} from "react";
import {createRoot} from "react-dom/client";
import {Fallback} from "./fallback";
import {Canvas} from "@react-three/fiber";
import {RoundedBox, OrbitControls} from "@react-three/drei";

type Position = [number, number, number];
function Block({at, size, color}: {at:Position;size:Position;color:string}) {
  return <RoundedBox args={size} position={at} radius={.04} smoothness={2}><meshStandardMaterial color={color}/></RoundedBox>;
}
function Desk() {
  const [night,setNight]=useState(document.documentElement.dataset.theme==="night");
  React.useEffect(()=>{
    const observer=new MutationObserver(()=>setNight(document.documentElement.dataset.theme==="night"));
    observer.observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
    return ()=>observer.disconnect();
  },[]);
  const select=(name:string)=>{
    const button=Array.from(document.querySelectorAll<HTMLButtonElement>(".workspace button")).find(el=>el.textContent===name);
    button?.click();
  };
  return <>
    <ambientLight intensity={night?.9:1.5}/><directionalLight position={[3,6,4]} intensity={2.1} color={night?"#e6cdee":"#fff0d7"}/>
    <Block at={[0,-.18,0]} size={[5,.28,3]} color="#dfbecf"/>
    <group onClick={()=>select("Laptop")}><Block at={[-.6,.08,.25]} size={[1.7,.13,1.1]} color="#bdabcb"/><Block at={[-.6,.67,-.28]} size={[1.7,1.12,.12]} color="#b298b6"/><Block at={[-.6,.68,-.19]} size={[1.48,.9,.03]} color="#514559"/>
    {[.8,.55,.7].map((w,i)=><Block key={i} at={[-.75,.9-i*.17,-.15]} size={[w,.035,.02]} color="#f0c7d6"/>)}</group>
    <group onClick={()=>select("Books")}>{[0,1,2].map(i=><Block key={i} at={[-1.8,.1+i*.16,-.5]} size={[.8,.13,.85]} color={i===1?"#afcee2":"#e4c4d3"}/>)}</group>
    <group onClick={()=>select("Cloud")} position={[1.2,1.6,-.6]}>{[-.35,0,.34].map((x,i)=><mesh key={i} position={[x,i===1?.16:0,0]}><sphereGeometry args={[.34,16,12]}/><meshStandardMaterial color="#f7eaf6"/></mesh>)}</group>
    <group onClick={()=>select("Mug")} position={[.9,.3,.47]}><mesh><cylinderGeometry args={[.28,.23,.55,20]}/><meshStandardMaterial color="#e4abc2"/></mesh><mesh position={[.26,.02,0]}><torusGeometry args={[.16,.045,8,18]}/><meshStandardMaterial color="#e4abc2"/></mesh></group>
    <group onClick={()=>select("Frame")}><Block at={[1.68,.49,-.65]} size={[.73,.85,.11]} color="#ab8f77"/><Block at={[1.68,.49,-.58]} size={[.58,.69,.03]} color="#cee1e5"/></group>
    <group onClick={()=>select("Notebook")}><Block at={[1.7,.05,.68]} size={[.7,.13,.83]} color="#c4b7db"/></group>
    <OrbitControls enableZoom={false} enablePan={false} minPolarAngle={.6} maxPolarAngle={1.3} minAzimuthAngle={-.65} maxAzimuthAngle={.75}/>
  </>;
}
export function mount(host:HTMLElement) {
  createRoot(host).render(<Fallback><Canvas role="img" aria-label="Interactive miniature coding desk. Use the buttons below to explore its objects." frameloop="demand" dpr={[1,1.5]} camera={{position:[3,3.5,5],fov:43}}><Desk/></Canvas></Fallback>);
}
