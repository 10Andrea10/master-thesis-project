export function convertProof(proof: string) {
  var mydata = JSON.parse(proof);
  // console.log(mydata);

  // convert input values (Fr-scalar-fields)
  for (let i = 0; i < mydata.inputs.length; i++) {
    mydata.inputs[i] = hexStringBig2LittleEndian(mydata.inputs[i]);
  }
  // convert proof (G1 and G2 curve points)
  mydata.proof.a = convert_array_2_G1point(mydata.proof.a);
  mydata.proof.b = convert_array_2_G2point(mydata.proof.b);
  mydata.proof.c = convert_array_2_G1point(mydata.proof.c);
  //console.log(mydata);

  return JSON.stringify(mydata, null, 4);
}

// converts an G1 point from uncompressed (Ethereum) into compressed form (Tezos)
function convert_array_2_G1point(arr: any) {
  var g1 = arr[0] + arr[1].substring(2, arr[1].length);
  return g1;
}

// converts an G2 point from uncompressed (Ethereum) into compressed form (Tezos)
function convert_array_2_G2point(arr: any) {
  var g2 =
    arr[0][1] +
    arr[0][0].substring(2, arr[0][0].length) +
    arr[1][1].substring(2, arr[0][0].length) +
    arr[1][0].substring(2, arr[0][0].length);
  return g2;
}

function hexStringBig2LittleEndian(hexString: any) {
  const hexString2ArrayReversed = hexStringToByteArray(hexString).reverse();

  return byteArrayToHexString(hexString2ArrayReversed);
}

function hexStringToByteArray(hexString: any) {
  var numBytes = hexString.length / 2;
  var byteArray = new Uint8Array(numBytes);
  for (var i = 0; i < numBytes; i++) {
    byteArray[i] = parseInt(hexString.substr(i * 2, 2), 16);
  }
  return byteArray;
}

function byteArrayToHexString(byteArray: any) {
  var hexString = '';
  var nextHexByte;
  for (var i = 0; i < byteArray.byteLength - 1; i++) {
    nextHexByte = byteArray[i].toString(16); // Integer to base 16
    if (nextHexByte.length < 2) {
      nextHexByte = '0' + nextHexByte; // Otherwise 10 becomes just a instead of 0a
    }
    hexString += nextHexByte;
  }
  return hexString;
}
