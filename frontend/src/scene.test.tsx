import React from "react";
import {render,screen} from "@testing-library/react";
import {expect,it,vi} from "vitest";
import {Fallback} from "./fallback";

it("keeps the illustrated desk available after a renderer error",()=>{
  const log=vi.spyOn(console,"error").mockImplementation(()=>{});
  function BrokenDesk():React.JSX.Element {throw new Error("Renderer unavailable");}
  try {
    render(<Fallback><BrokenDesk/></Fallback>);
    expect(screen.getByRole("img",{name:"Illustrated coding desk"}).getAttribute("src")).toBe("/art/workspace.svg");
  } finally {log.mockRestore();}
});
