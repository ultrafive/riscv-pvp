# RISC-V PVP

RISC-V PVP is a modular and parameterized RISC-V Processor Verification Platform.

It currently supports the following features:

- Supported RISC-V ISA:
    - RV32G
    - RV64G
    - C Extension, 2.0
    - V Extension, 0.10
- YAML based hand-written sequence templates
- numpy based golden data for vector ISA
- Easy to support new ISAs
- Easy to add new cases
- End-to-end RTL&ISS co-simulation flow

## Motivation

Open source RISC-V processor verification solutions such as riscv-tests,
riscv-arch-test have provided good sanity verifications for RISCV basic ISAs,
but new extensions(for example, Vector, Bitmanip) support is missing.

Our motivation is build a high quality open source verification platform to
support more extensions easily to improve the verification quality of RISC-V
processors.

## Issues

Please file an issue under this repository for any bug report / integration
issue / feature request. We are looking forward to knowing your experience of
using this flow and how we can make it better together.

## License

MIT License

Copyright © 2020-2021 UltraFive Team

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.