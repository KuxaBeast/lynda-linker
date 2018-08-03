// ==UserScript==
// @name         LyndaLinkerScript
// @namespace    http://tampermonkey.net/
// @version      0.4
// @description  This script allows multiple users to watch videos from lynda.com for free with help of assisting server
// @author       KuxaBeast
// @grant        none
// @include      https://www.lynda.com*
// ==/UserScript==

(function () {
  'use strict'

  let solverAdress = 'http://example.com/'

  let lasturl = null
  let currenturl = window.location.href

  let linker = {}

  function createLinkerPanel(linker) {
    linker.panel = document.createElement('div')
    styleElement(linker.panel, {position: 'fixed', backgroundColor: 'white', bottom: '0px', right: '50px', padding: '5px', zIndex: '2000000'})

    document.body.appendChild(linker.panel)

    linker.form = createForm()
    linker.panel.appendChild(linker.form)
  }

  function createForm() {
    let form = document.createElement('form')
    form.action = solverAdress
    form.method = 'post'
    form.target = '_blank'

    let dlbtn = document.createElement('input')
    styleElement(dlbtn, {fontSize: '12px', color: '#C000C0', border: '1px solid #CCCCCC', borderRadius: '3px', cursor: 'pointer', padding: '0px 5px'})
    dlbtn.type = 'submit'
    dlbtn.value = 'Play'
    form.appendChild(dlbtn)

    let url = document.createElement('input')
    url.type = 'hidden'
    url.name = 'lyndaurl'
    url.value = currenturl
    form.appendChild(url)

    let qual = document.createElement('input')
    qual.type = 'hidden'
    qual.name = 'quality'
    qual.value = '540'
    form.appendChild(qual)

    return form
  }

  function styleElement(obj, styles) {
    for (let property in styles) {
      if (styles.hasOwnProperty(property)) obj.style[property] = styles[property];
    }
  }

  function setVisible(element, visible) {
    if (visible) element.style.display = 'initial'
    else element.style.display = 'none'
  }

  function removePanel() {
    document.body.removeChild(linker.panel)
  }

  function hideTrialAds() {
    let toHide = []
    toHide.push(document.getElementsByClassName("top-cta")[0])
    toHide.push(document.getElementById("sub-nav"))
    toHide.push(document.getElementsByClassName("bottom-cta")[0])

    console.log(toHide)
    
    toHide.forEach(element => {
      //console.log(element)
      if (element != null) {
        element.style.display = 'none'
      }
    })
  }

  function replacePlayer() {
    let videoParent = document.getElementById('video-container')
    videoParent.querySelectorAll('*').forEach(element => {
      //element.style.visibility = 'hidden'
      element.style.display = 'none'
    })

    let oldvideo = videoParent.getElementsByTagName('video')[0]
    oldvideo.pause()

    if (videoParent.getElementsByClassName('cplayer')[0] != null) {
      videoParent.removeChild(videoParent.getElementsByClassName('cplayer')[0])
    }

    //console.log(videoParent.getElementsByTagName('video'))

    let player = document.createElement('video')
    player.className = 'cplayer'
    //player.style.position = 'absolute'
    //player.style.top = '0px'
    player.width = videoParent.clientWidth
    player.controls = true
    player.autoplay = true

    let source = document.createElement('source')
    source.src = getVideoUrl(solverAdress, currenturl, "720")
    source.type = 'video/mp4'
    player.appendChild(source)

    videoParent.appendChild(player)
  }

  function getVideoUrl(solver, page_url, quality) {
    let out = solver
    if (!out.endsWith("/")) out += "/"
    out += "?"
    out += "courseid=" + page_url.split('/')[5]
    out += "&"
    out += "videoid=" + page_url.split("/")[6].split(".")[0]
    out += "&"
    out += "qual=" + quality
    return out
  }

  window.setInterval(function () {
    if (currenturl != window.location.href || lasturl == null) {
      lasturl = currenturl
      currenturl = window.location.href

      let url = currenturl.split('/')
      if (!(url[0] == 'https:' && url[2] == 'www.lynda.com' && Number.isInteger(Number(url[5])) && Number.isInteger(Number(url[6].split('-')[0])))) {
        //setVisible(linker.panel, false)
      } else {
        //setVisible(linker.panel, true)
        replacePlayer()
      }

      hideTrialAds()
    }
  }, 500)

  //createLinkerPanel(linker)

})();
