import React from "react";
import {render,screen} from "@testing-library/react";
import {expect,it} from "vitest";
import {readFileSync} from "node:fs";
it("provides a named island for every configured project",()=>{
  const {projects}=JSON.parse(readFileSync("../content/portfolio.json","utf8"));
  render(<nav>{projects.map((p:{slug:string;name:string})=><a key={p.slug} href={"/projects/"+p.slug}>{p.name}</a>)}</nav>);
  expect(screen.getAllByRole("link")).toHaveLength(4);
});
