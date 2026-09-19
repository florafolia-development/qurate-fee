import { describe, it, expect } from "vitest";
import { devBypassAllowed } from "@/lib/tokenUtils";

describe("devBypassAllowed", () => {
  it("lets a development build bypass with ?dev=true", () => {
    expect(devBypassAllowed("true", true)).toBe(true);
  });

  it("refuses the bypass in a deployed build, which is the whole point", () => {
    expect(devBypassAllowed("true", false)).toBe(false);
  });

  it("refuses anything that is not exactly 'true'", () => {
    expect(devBypassAllowed("TRUE", true)).toBe(false);
    expect(devBypassAllowed("1", true)).toBe(false);
    expect(devBypassAllowed("", true)).toBe(false);
    expect(devBypassAllowed(null, true)).toBe(false);
  });
});
