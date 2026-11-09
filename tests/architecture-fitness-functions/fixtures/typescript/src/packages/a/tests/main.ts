import { read } from "../index";
import { fixture } from "./fixture";
import { calculate } from "../../b/index";
export const check = () => [read(), fixture, calculate()];
