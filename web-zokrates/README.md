# Web-Rollup

This is the web server used for compute the rollup using the Zokrates toolbox.

## Pre-requisites

A Zokrates compiled program, together with the proving key and the abi specification must be present in the `src/zokrates` folder.

## Installation

The installation of the web server is done using the following command:

```
npm install
npm start
```

## Usage

The web server is listening on port 3005. The following endpoints are available:

- `/execute` : expects in the body the inputs of the Zokrates program. NOTE: the content-type must be `text/plain`