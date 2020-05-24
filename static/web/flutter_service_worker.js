'use strict';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "index.html": "0c880c73285ad8591772dda9dab59977",
"/": "0c880c73285ad8591772dda9dab59977",
"main.dart.js": "432709d695cc11b76a8555a6a5358541",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"manifest.json": "cdb648de8badcfb42f87f0e187b755a3",
"assets/LICENSE": "4471cefa11a047f5a35b52d72fbca5de",
"assets/images/svg/default_album.svg": "f4c0e22fee71a7d7c76ac8ca9fc88b9f",
"assets/images/svg/ifl.svg": "d4fa96c9c4c323859e3b21c93776e8f3",
"assets/images/svg/splash_screen.svg": "cfefcb9a217dc191d15a6232f9d1557f",
"assets/images/background_image/bfb2ff.png": "d9511a1ec3bc647c0aae8700af253420",
"assets/images/background_image/4b2460.png": "ece781997def0de2783366860751825b",
"assets/images/background_image/c6fbe5.png": "a8b0e111bcc05d4167ede19fa3975e70",
"assets/images/background_image/4bceff.png": "370c2efa7144c2fbb566ba084f90a5bf",
"assets/images/background_image/54215f.png": "018da8f9e9bdad26b3e06415f8fdd7d4",
"assets/images/background_image/531e65.png": "e2271cf5bb81d35a78127b6f920103ee",
"assets/images/background_image/5dced6.png": "506efc9cdd332bf30e9cff22dd8ef917",
"assets/images/background_image/532164.png": "2ceba1ec91991efd7ab993a8c4dd4a76",
"assets/images/background_image/47c7fe.png": "8e7481600b2d56bd8d4e96adc3fd6f71",
"assets/images/background_image/19ba6a.png": "67cf249a79364a436a7004675e99ec9c",
"assets/images/background_image/63230a.png": "a8117ef41095319740e1b000e2e109bb",
"assets/images/background_image/1ee8b6.png": "1d6d412698c4edbfca4baaf02a2f127c",
"assets/images/background_image/12b969.png": "6b93535b60d792c1fe3ebcde718ea81c",
"assets/images/background_image/512257.png": "7582d744a9ca41e57bcc0ccb1c01441e",
"assets/images/background_image/4413ba.png": "1b23dd9314e64ea8202042974b06f2a3",
"assets/images/background_image/17316d.png": "999d593e0b23ae60c2642cca55e56e93",
"assets/images/background_image/392291.png": "68b60651e7c1572701fad02a5eac18f7",
"assets/images/default_album.jpg": "93ce9a82076643df56f136967e46e328",
"assets/images/colored_now_card.jpg": "73107ba777cb6fd8f2661e92d93998df",
"assets/images/home.jpg": "7c8c56f04bfe2934b55eb21961dbef5f",
"assets/images/backgroundImages/1aN6mX4KtTKKOBfGwSftr-hxuHhHIUyxPoN7R1fEZYwZ02GrVCONCTQxtbLWxF85rUs49HCMaQ.png": "b2c97c1e25e3482f89b67b95a4a21079",
"assets/images/backgroundImages/xLasi4eSHmkP_Fl0bVuDhvjiS9F6LihKFHa20lpO_9whutIgzfTMoPhxaxRKtlcqpbKyCA_cSTQ.png": "8a58fac20929afde703a4300582c6351",
"assets/images/backgroundImages/HAS6pzVdYATF4MbFw6ZOhsLp8cU7D7qVj2jEtD5YzlXnVQyTUzcIs0O8KShMVoZa4bUOcnUC0w.png": "e1cd43d995cc20f4e80c9c3ee380b3bc",
"assets/images/backgroundImages/EgjW-j_s1J68IH6GIbxGd2sDNtvipdKPLjC-Nf3CZ41zzJuae7Y2UzsKVJdhYlyesID2RZVz.png": "a49c0fd4285905191ef947d7f77ec2ce",
"assets/images/backgroundImages/backgroundImages.json": "7f929236114c8adb6a5899ea801f40a8",
"assets/images/backgroundImages/3rSsn09XlksGOUhWrgB7vSJwPWzmlS0Zp7FZZ1o1cipRdFyJ_mQ0bbXg6KKeNaebF1OiXZKz.png": "005c11733360552a282285631810449e",
"assets/images/backgroundImages/maUoAOgHshpBAeTDmkULhnMe-8oGljo1TdCDMdUtY0jNEZ5iR3B6hhc6-Ghvuft-sOR0LXrAxA4.png": "a394abc872b5e8b3003e10829e8cdf01",
"assets/images/backgroundImages/kkSI0jxnAYZ6_3jeLT7aZ9A9ITBaA5MQjGNS1jmhtdSCorKCgouBuUXg1Yvktfb_l6wflXDiFWI.png": "8934f7df4cc1fd4cc1c653a192872568",
"assets/images/backgroundImages/f-m-m5tQ9knrY3lPJQgFFhrdeoefL3FzY2SgEQjkxPP2HlcsI1FQd9A-Yxj8_HIOqjYPhrLf.jpg": "85a7c8dab9e99a300b9550d379715d20",
"assets/images/backgroundImages/HyaLITKzgLGwFY90pKkHW7fxiBaCko9kZB6awnDk2FQYb4iBq9Ndoj5fr0DCH2CmQLskFaZh.png": "03fea785f4629d310a426c21fbad8048",
"assets/images/backgroundImages/WwnaSyZar1s7gJWNsjWf-xmaLDDKpSs4i4bkbMtWGqFj24m-ucOwj3ltVjVy6NUsy5fTprCY.png": "f462571caf4d755e8731dd43825e455f",
"assets/images/sj_dot.png": "60f95e4a16f39b7b6821045b15e5e1fa",
"assets/images/lake.jpg": "236690c07321de26550682c399675fb4",
"assets/images/ifl.png": "c96498ff806766716ef3eb830bf9acf6",
"assets/images/illo_default_artistradio_smallcard.png": "31db16b00b6ead3c8cb894fb6109d099",
"assets/images/2x/illo_default_artistradio_smallcard.png": "cecc1bcd51b3da7bcd0a7f5abab471a7",
"assets/images/1x/illo_default_artistradio_smallcard.png": "31db16b00b6ead3c8cb894fb6109d099",
"assets/AssetManifest.json": "7342fd648580cf6268c8e087822ee5c4",
"assets/FontManifest.json": "01700ba55b08a6141f33e168c4a6c22f",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "115e937bb829a890521f72d2e664b632",
"assets/fonts/MaterialIcons-Regular.ttf": "56d3ffdef7a25659eab6a68a3fbfaf16"
};

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheName) {
      return caches.delete(cacheName);
    }).then(function (_) {
      return caches.open(CACHE_NAME);
    }).then(function (cache) {
      return cache.addAll(Object.keys(RESOURCES));
    })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
