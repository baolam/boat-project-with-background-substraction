const max_ntu = 10000;
const max_tds = 10000;
const max_ph = 14;
function standardlize(feature)
{
  feature[0] /= max_ntu;
  feature[1] /= max_tds;
  feature[2] /= max_ph;
  return feature;
}

module.exports = standardlize;