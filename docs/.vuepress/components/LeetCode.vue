<template>
  <div class="leetcode">
    <a-spin size="large" tip="Loading..." :spinning="!ranking">
      <p v-if="rating" class="rating">{{ isEnglishSite? "Rating": "竞赛积分" }}: {{ rating }}</p>
      <p v-if="CNranking" class="ranking">
        {{ isEnglishSite? "Rating": "竞赛积分" }}: {{ CNranking }}
      </p>
      <p v-if="ranking" class="ranking">{{ isEnglishSite? "Global Ranking": "全球排名" }}: {{ ranking }}</p>
      <div id="chart">
        <svg></svg>
      </div>
    </a-spin>
  </div>
</template>

<script>
import { useSiteLocaleData } from '@vuepress/client';
// import { onBeforeMount } from 'vue';
import { axiosCorsProxy } from '../axios-instances';
// import * as d3 from 'd3';
// import * as nvd3 from 'nvd3';
import * as d3 from './assets/js/d3.min.js'


export default {
  props: {
    lang: {
      type: String,
      required: false,
    },
  },
  computed: {
    siteLocale() {
      return useSiteLocaleData();
    },
    isEnglishSite() {
      return ["en", "en-us"].includes(this.siteLocale.value.lang.toLowerCase());
    },
  },
  data() {
    return {
      ranking: null,
      rating: null,
      CNranking: null,
    };
  },
  beforeMount() {
    // ranking details from global site
    // await import('./test')
    // await import('d3');
    // await import('nvd3');
    axiosCorsProxy
      .get("", { params: { url: "https://leetcode.com/lucienzhang/" } })
      .then(res => {
        console.log('TEST',res);
        return axiosCorsProxy.post("",
          {
            operationName: "getContentRankingData",
            variables: { username: "lucienzhang" },
            query: `
query getContentRankingData($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    __typename
  }
  userContestRankingHistory(username: $username) {
    contest {
      title
      startTime
      __typename
    }
    rating
    ranking
    __typename
  }
}
`,
          },
          {
            params: {
              url: "https://leetcode.com/graphql", headers: {
                referer: "https://leetcode.com/lucienzhang/",
                cookie: res.data.headers['set-cookie'].split(';')[0]
              },
            },
          })
      })

      // axios
      //   .post(
      //     "https://cors-anywhere.herokuapp.com/https://leetcode.com/graphql",
      //     {
      //       operationName: "getContentRankingData",
      //       variables: { username: "lucienzhang" },
      //       query:
      //         "query getContentRankingData($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    __typename\n  }\n  userContestRankingHistory(username: $username) {\n    contest {\n      title\n      startTime\n      __typename\n    }\n    rating\n    ranking\n    __typename\n  }\n}\n",
      //     },
      //     {
      //       headers: {
      //         authority: "leetcode.com",
      //         accept: "*/*",
      //         "content-type": "application/json",
      //         // origin: "https://leetcode.com",
      //         // "sec-fetch-site": "same-origin",
      //         // "sec-fetch-mode": "cors",
      //         // "sec-fetch-dest": "empty",
      //         // referer: "https://leetcode.com/lucienzhang/",
      //         "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
      //       },
      //     }
      //   )
      .then((res) => {
        let data = res.data.data;
        this.ranking = data.userContestRanking.globalRanking;
        this.rating = parseInt(data.userContestRanking.rating);

        let ranking_data = [{ values: [], key: "Rating", color: "#ff7f0e" }];

        data.userContestRankingHistory.forEach(function (node, i) {
          ranking_data[0].values.push({
            x: i,
            y: parseInt(node.rating),
            contest_title: node.contest.title,
            ranking: node.ranking,
          });
        });

        nvd3.addGraph(function () {
          let chart = nvd3.models
            .lineChart()
            .useInteractiveGuideline(false)
            .margin({ top: 20, right: 20, bottom: 40, left: 55 });

          chart.xAxis.axisLabel("Contest Number");

          chart.yAxis
            .axisLabel("Rating")
            .tickFormat(d3.format(".00f"))
            .axisLabelDistance(-10);

          chart.tooltip.contentGenerator(function (e) {
            let ranking =
              '<p style="text-align: left;">Ranking: <strong>' +
              e.point.ranking +
              "</strong></p>";
            if (e.point.ranking == 0) {
              ranking = '<p style="text-align: left;">Not Attended</p>';
            }
            return (
              '<div><p style="text-align: left;">' +
              e.point.contest_title +
              '</p></div><div><p style="text-align: left;">Rating: <strong>' +
              e.point.y +
              "</strong></p>" +
              ranking +
              "</div>"
            );
          });

          d3.select("#chart svg").datum(ranking_data).call(chart);

          //Update the chart when window resizes.
          nvd3.utils.windowResize(function () {
            chart.update();
          });
          return chart;
        });
      })
      .catch((res) => {
        console.log(res);
      });

    // CN ranking from CN site
    axiosCorsProxy
      .post("",
        {
          operationName: "userContest",
          variables: { username: "lucien_z" },
          query: `
query userContest($userSlug: String!) {
  userContestRanking(userSlug: $userSlug) {
    currentRatingRanking
    __typename
  }
}
`,
        },
        { params: { url: "https://leetcode-cn.com/graphql" } })
      // axios
      //   .post(
      //     "https://cors-anywhere.herokuapp.com/https://leetcode-cn.com/graphql/",
      //     {
      //       operationName: "userContest",
      //       variables: { userSlug: "lucien_z" },
      //       query:
      //         "query userContest($userSlug: String!) {\n  userContestRanking(userSlug: $userSlug) {\n    currentRatingRanking\n    __typename\n  }\n}\n",
      //     },
      //     {
      //       headers: {
      //         authority: "leetcode-cn.com",
      //         accept: "*/*",
      //         "content-type": "application/json",
      //         // origin: "https://leetcode.com",
      //         // "sec-fetch-site": "same-origin",
      //         // "sec-fetch-mode": "cors",
      //         // "sec-fetch-dest": "empty",
      //         // referer: "https://leetcode.com/lucienzhang/",
      //         "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
      //       },
      //     }
      //   )
      .then((res) => {
        this.CNranking = res.data.data.userContestRanking.currentRatingRanking;
      })
      .catch((res) => {
        console.log(res);
      });
  },
};
</script>

<style lang="scss" scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css");

.leetcode {
  .ranking {
    font-weight: bold;
    font-size: 1.3em;
    color: #ef4743;
  }

  .rating {
    font-weight: bold;
    font-size: 1.3em;
    color: rgb(255, 127, 14);
  }

  #chart svg {
    height: 450px;
  }
}
</style>
