/**
 * 
 * @param {*} target_feature 
 * @param {*} source_feature
 * @description
 * Tính toán khác biệt giữa 2 đặc trưng đầu vào
 * @essential
 * Khoảng cách euclid 
 */
function differentation(target_feature, source_feature)
{
  let r = 0, n = target_feature.length;
  if (n != source_feature.length)
    return Infinity;
  for (let i = 0; i < n; i++)
    r = r + Math.pow(
      (target_feature[i] - source_feature[i]), 
    2);
  r = Math.sqrt(r);
  return r;
}

const { recommend_events, EVENTS } = require("../config/events/recommend");
class Recommender {
  constructor()
  {
    /// Ngưỡng khác biệt nhỏ nhất để chấp nhận
    this.theta = 0.4;

    /// Những sự kiện
    recommend_events.addListener(EVENTS.UPDATE_THETA, (theta) => this.__update_theta(theta));
  }

  /**
   * 
   * @param {*} theta
   * @private
   * @method
   * Cập nhật ngưỡng khác biệt 
   */
  __update_theta(theta)
  {
    this.theta = theta;
  }

  /**
   * 
   * @param {*} target_source 
   * @param {*} recommend_sources 
   * @method
   * Xác định đối tượng có sự khác biệt là nhỏ nhất
   * Nhóm các đối tượng tương tự
   * @returns 
   */
  run(target_source, recommend_sources)
  {
    let goal = 0, differentation_value = Infinity;
    let similars = [];

    for (let i = 0; i < recommend_sources.length; i++)
    {
      let result = differentation(target_source, recommend_sources[i]);
      if (result <= this.theta)
      {
        /// Thêm nhóm đối tượng mà nằm trong ngưỡng chấp nhận được
        similars.push({
          similar_id : i,
          result
        });

        /// Lấy đối tượng đem ra đề xuất (tìm kiếm GTNN)
        if (result < differentation_value)
        {
          differentation_value = result;
          goal = i;
        }
      }
    }

    return {
      goal,
      differentation : differentation_value,
      similars
    }
  }
}

module.exports = Recommender;