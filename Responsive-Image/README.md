# Responsive Images:
[Responsive Images](https://linxuedong.github.io/Udacity-Project/Responsive-Image/)

## 笔记

- `npm install`

- `grunt`

- `python -m SimpleHTTPServer` 启动简单 HTTP 服务器

## ImageMagick
[ImageMagick download](https://www.imagemagick.org/script/download.php#macosx)
`brew install ImageMagick`

## 字符与矢量图标
* [Unicode® character table](https://unicode-table.com/en/)
* [Zocial | CSS3 Button Set](http://zocial.smcllns.com/)

## 对于响应式图片，我们需要关心三个变量：

* 布局中图片的渲染尺寸（CSS 像素尺寸）
* 像素密度
* 我们手头可支配的不同尺寸的图片
> The rendered size (in CSS pixels) of the image on our layout  
> The screen density  
> The dimensions of the variously-sized files at our disposal

## srcset + sizes
```html
<img src="small.jpg"
	 srcset="large.jpg 1024w,
			 medium.jpg 640w,
			 small.jpg 320w"
 	 sizes="(min-width: 30em) 100vw,
			33.33vw"
	 alt="responsive image">
```
src 当浏览器不支持 srcset 属性，加载 small.jpg  
srcset: 为不同尺寸适用不同的 图片  
sizes: *属性为浏览器提供了有关图片元素显示大小的信息，它实际上不会导致图片大小调整。该操作是在 CSS 中执行的！*

[Srcset 和 sizes](https://blog.zfanw.com/srcset-and-sizes/)

## picture
```html
<picture>
	<source media="(min-width: 750px)" srcset="image_1600_large_2x.jpg 2x, image_800_large_1x.jpg" />
	<source media="(min-width: 500px)" srcset="medium.jpg" />
	<img src="small.jpg" alt="Horses in Hawaii">
</picture>
```
