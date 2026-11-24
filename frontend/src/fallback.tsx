import React, {Component} from "react";
export class Fallback extends Component<{children:React.ReactNode},{failed:boolean}> {
  state={failed:false};
  static getDerivedStateFromError(){return {failed:true};}
  render(){return this.state.failed?<img src="/art/workspace.svg" alt="Illustrated coding desk"/>:this.props.children;}
}
