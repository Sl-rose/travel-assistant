export async function fetchSSE(url, options, onMessage) {
	const customHeaders = (options && options.headers) || {};
	const response = await fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
			...customHeaders
		},
		body: new URLSearchParams(options.body)
	});

	const reader = response.body.getReader();
	const decoder = new TextDecoder("utf-8");

	while (true) {
		const {
			value, 
			done
			} = await reader.read();
		if (done) break;
		const chunk = decoder.decode(value, {
			stream: true
	});
	// 服务端 SSE 一般格式:"data: xxx\n\n"
	chunk.split("\n\n").forEach(line => {
		if (line.startsWith("data:")) {
			// 去掉 "data:" 并去除首尾空格
			let content = line.slice(5).trimStart();
			// 将编码的换行符还原
			content = content.replace(/\\n/g, '\n');
			onMessage(content);
		}
	});
}
}