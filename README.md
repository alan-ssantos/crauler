```json
{
	"config": {
		"test": true, // true: irá executar o scrapper em apenas três links. false: irá executar o scrapper em todos os links.
		"base_url": "https://www.domain.com/",
		"base_description": "Lorem ipsum dolor sit amet consectetur adipisicing elit.",
		"page_category_name": "produtos", // produtos ou blog (a categoria blog ainda não é suportado por este scrapper)
		"category_id": 1, // ID da categoria de produtos ou blog (pode ser diferente, dependendo da ordem que foram cadastradas)
		"categories": [], // Lista de nomes das categorias, precisam ser iguais aos que vão ser encontrados pelo seletor `category`
		"product_id": 1, // ID inicial dos produtos/blog, será utilizado para relacionar a galeria de imagens e downloads
		"download_category_id": 5, // ID da categoria downloads (pode ser diferente, dependendo da ordem que foi cadastrada)
		"current_download_id": 1 // ID inicial dos arquivos de download, será incrementado conforme a quantidade de downloads encontrados
	},
	"selectors": {
		// Seletores vazios ou nulos são permitidos apenas em atributos opcionais
		"page_title": ".title",
		"page_cover": ".cover",
		"old_price": null,
		"new_price": null,
		"category": null, // Não definir significa que todas páginas são da categoria inicial, definida em `category_id`
		"publish_date": null,
		"page_content": ".main-content",
		"page_short_description": ".intro",
		"gallery": ".slider a",
		"downloads": ".downloads a"
	},
	"links": [
    "https://www.domain.com/products/1",
    "https://www.domain.com/products/2"
  ]
}


```