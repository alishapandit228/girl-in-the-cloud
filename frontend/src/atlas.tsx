import React, {useRef, useState} from "react";
import {createRoot} from "react-dom/client";
import {Canvas, useFrame} from "@react-three/fiber";
import {OrbitControls, RoundedBox} from "@react-three/drei";
import {Group, Mesh} from "three";
import {Fallback} from "./fallback";

function Servers({at, count}:{at:[number,number,number];count:number}){
  return <group position={at}>{Array.from({length:count},(_,index)=>
    <group key={index} position={[0,.16+index*.36,0]}>
      <RoundedBox args={[.74,.31,.86]} radius={.05} smoothness={2}><meshStandardMaterial color={index%2?"#d2c0dd":"#c6d8e6"}/></RoundedBox>
      <mesh position={[-.06,0,.44]}><boxGeometry args={[.49,.07,.02]}/><meshStandardMaterial color="#6d6179"/></mesh>
      <mesh position={[.25,.02,.44]}><sphereGeometry args={[.04,8,8]}/><meshStandardMaterial color="#fff0c2" emissive="#d79a62" emissiveIntensity={.65}/></mesh>
    </group>)}</group>;
}
function Network(){
  const cloud=useRef<Group>(null);
  const packet=useRef<Mesh>(null);
  useFrame(({clock})=>{
    const time=clock.elapsedTime;
    if(cloud.current)cloud.current.position.y=Math.sin(time*.8)*.045;
    if(packet.current)packet.current.position.x=-1.15+((time*.42)%1)*2.3;
  });
  return <group ref={cloud}>
    {Array.from({length:12},(_,i)=>{
      const a=i*Math.PI/6;
      return <mesh key={i} position={[1.86*Math.cos(a),-.31,1.12*Math.sin(a)]} scale={[.94,.48,.78]}>
        <sphereGeometry args={[1,18,12]}/><meshStandardMaterial color={i%2?"#f6e9f4":"#e7dbea"}/>
      </mesh>;
    })}
    <RoundedBox args={[3.8,.15,2.45]} radius={.07} smoothness={2}><meshStandardMaterial color="#c9b5d2"/></RoundedBox>
    <Servers at={[-1.12,.07,-.15]} count={4}/><Servers at={[.05,.07,-.57]} count={3}/><Servers at={[1.18,.07,-.15]} count={5}/>
    <mesh position={[0,.13,.67]}><boxGeometry args={[2.65,.035,.04]}/><meshStandardMaterial color="#9c829e"/></mesh>
    <mesh ref={packet} position={[0,.18,.67]}><sphereGeometry args={[.075,10,8]}/><meshStandardMaterial color="#fff5cf" emissive="#f0c294"/></mesh>
  </group>;
}
function Atlas(){
  const [night,setNight]=useState(document.documentElement.dataset.theme==="night");
  React.useEffect(()=>{
    const watch=new MutationObserver(()=>setNight(document.documentElement.dataset.theme==="night"));
    watch.observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});return()=>watch.disconnect();
  },[]);
  return <Canvas aria-label="Cloud island with connected server racks" role="img" dpr={[1,1.4]} camera={{position:[4.9,3.3,5.5],fov:44}}>
    <ambientLight intensity={night?.85:1.55}/><directionalLight intensity={2.4} position={[3,5,3]} color={night?"#dcc7ed":"#fff0d9"}/>
    <Network/><OrbitControls enablePan={false} enableZoom={false} minPolarAngle={.65} maxPolarAngle={1.35}/>
  </Canvas>;
}
export function mountAtlas(host:HTMLElement){
  const root=createRoot(host);
  root.render(<Fallback><Atlas/></Fallback>);
  return ()=>root.unmount();
}
