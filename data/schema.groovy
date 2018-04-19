// graph schema
// 不加索引，不加cache
// 2018年04月12日12:05:02

// 删除schema和所有data，不删除graph
schema.clear()

// 属性
schema.propertyKey("name").Text().create()  // 名称，唯一
schema.propertyKey("drug_category").Text().create()  // 药物类别（中药/西药）
schema.propertyKey("approval_number").Text().create()  // 批准文号
schema.propertyKey("component").Text().create()  // 成份
schema.propertyKey("character").Text().create()  // 性状
schema.propertyKey("indication").Text().create()  // 适应症
schema.propertyKey("manufacturer").Text().create()  // 生产厂商
schema.propertyKey("main_cure").Text().create()  // 主治疾病
schema.propertyKey("effect_type").Text().create()  // 作用类别
schema.propertyKey("untoward_reaction").Text().create()  // 不良反应
schema.propertyKey("taboo").Text().create()  // 禁忌
schema.propertyKey("standard").Text().create()  // 执行标准
schema.propertyKey("product_name").Text().create()  // 商品名称
schema.propertyKey("usage").Text().create()  // 用法用量
schema.propertyKey("notes").Text().create()  // 注意事项
schema.propertyKey("storage").Text().create()  // 贮藏
schema.propertyKey("drug_interactions").Text().create()  // 药物相互作用
schema.propertyKey("pharmacology").Text().create()  // 药理毒理
schema.propertyKey("overdose").Text().create()  // 药物过量
schema.propertyKey("warning").Text().create()  // 警告
schema.propertyKey("for_olds").Text().create()  // 老年用药
schema.propertyKey("for_children").Text().create()  // 儿童用药
schema.propertyKey("dosage_form").Text().create()  // 剂型
schema.propertyKey("validity").Text().create()  // 有效期
schema.propertyKey("specification").Text().create()  // 规格
schema.propertyKey("for_pregnant").Text().create()  // 孕妇及哺乳期妇女用药
schema.propertyKey("revision_date").Text().create()  // 说明书修订日期
schema.propertyKey("pharmacokinetics").Text().create()  // 药代动力学
schema.propertyKey("packaging").Text().create()  // 包装
schema.propertyKey("URL").Text().create()  // url
schema.propertyKey("doc_id").Text().create()  // 文献编号
schema.propertyKey("title").Text().create()  // 文献题目
schema.propertyKey("medicine").Text().create()  // 文献涉及药物
schema.propertyKey("content").Text().create()  // 文献内容
schema.propertyKey("other").Text().create()  // 文献其他

// schema.propertyKey("clinical_test").Text().create()  // 临床试验
// schema.propertyKey("english_name").Text().create()  // 英文名称
// schema.propertyKey("pinyin").Text().create()  // 汉语拼音（太少）


// 节点类型
schema.vertexLabel("drug").properties("name", "drug_category").create()  // 药物通用名称
schema.vertexLabel("disease").properties("name").create()  // 疾病
schema.vertexLabel("component").properties("name").create()  // 成份
schema.vertexLabel("manufacturer").properties("name").create()  // 生产厂商
schema.vertexLabel("dispensatory").properties("name", "approval_number", "component", "character", "indication", "manufacturer", "main_cure", "effect_type", "untoward_reaction", "taboo", "standard", "product_name", "usage", "notes", "storage", "drug_interactions", "pharmacology", "overdose", "warning", "for_olds", "for_children", "dosage_form", "validity", "specification", "for_pregnant", "revision_date", "pharmacokinetics", "packaging", "URL").create()  // 药品说明书
schema.vertexLabel("document").properties("doc_id", "title", "medicine", "content", "other", "URL").create()  // 参考文献

// 关系
schema.edgeLabel("禁忌").connection("drug","drug").create()  // 药物——药物
schema.edgeLabel("治疗").connection("drug", "disease").create()  // 药物——疾病
schema.edgeLabel("含有").connection("drug", "component").create()  // 药物——成份
schema.edgeLabel("生产厂商").properties("approval_number").connection("drug","manufacturer").create()  // 药物——生产厂商
schema.edgeLabel("说明书").connection("drug","dispensatory").create()  // 药物——说明书
schema.edgeLabel("相关文献").connection("drug","document").create()  // 药物——相关文献

// 索引
schema.vertexLabel("disease").index("by_dis_name").secondary().by("name").add()
schema.vertexLabel("drug").index("by_drug_name").secondary().by("name").add()
schema.vertexLabel("drug").index("bycategory").secondary().by("drug_category").add()
schema.vertexLabel("component").index("by_com_name").secondary().by("name").add()
schema.vertexLabel("manufacturer").index("by_manu_name").secondary().by("name").add()
schema.vertexLabel("dispensatory").index("by_disp_name").secondary().by("name").add()
schema.vertexLabel("document").index("by_doc_id").secondary().by("doc_id").add()

// 缓存
schema.vertexLabel('drug').cache().properties().ttl(3600).add()
