'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "favicon.ico": "27ad2db051a0458935d59ba8142aaf3e",
"index.html": "930381bbd851c77442d994d0734ee8d1",
"/": "930381bbd851c77442d994d0734ee8d1",
"main.dart.js": "82ca7aad765e226e9b9d49e947815c2d",
"favicon.bak.png": "5dcef449791fa27946b3d35ad8803796",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"manifest.json": "5a886b0b86db9fa6ed17d8edeba31a9f",
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
"assets/images/backgroundImages/backgroundImages.json": "21e5ac0204318443c2fea43e8008a4c7",
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
"assets/NOTICES": "00bd00c18099e57f0871942157a2d8e6",
"assets/FontManifest.json": "01700ba55b08a6141f33e168c4a6c22f",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "115e937bb829a890521f72d2e664b632",
"assets/fonts/MaterialIcons-Regular.ttf": "56d3ffdef7a25659eab6a68a3fbfaf16"
};

// The application shell files that are downloaded before a service worker can
// start.
const CORE = [
  "/",
"main.dart.js",
"index.html",
"assets/LICENSE",
"assets/AssetManifest.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      // Provide a no-cache param to ensure the latest version is downloaded.
      return cache.addAll(CORE.map((value) => new Request(value, {'cache': 'no-cache'})));
    })
  );
});

// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');

      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        return;
      }

      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});

// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#')) {
    key = '/';
  }
  // If the URL is not the the RESOURCE list, skip the cache.
  if (!RESOURCES[key]) {
    return event.respondWith(fetch(event.request));
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache. Ensure the resources are not cached
        // by the browser for longer than the service worker expects.
        var modifiedRequest = new Request(event.request, {'cache': 'no-cache'});
        return response || fetch(modifiedRequest).then((response) => {
          cache.put(event.request, response.clone());
          return response;
        });
      })
    })
  );
});

self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.message == 'skipWaiting') {
    return self.skipWaiting();
  }

  if (event.message = 'downloadOffline') {
    downloadOffline();
  }
});

// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey in Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.add(resourceKey);
    }
  }
  return Cache.addAll(resources);
}
