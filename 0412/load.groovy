// DATA INPUT
// 更新时间：2018年04月12日13:51:02

inputfiledir = '0412'

drugs = inputfiledir+'/药物节点'
manufacturers = inputfiledir+'/生产厂商'
components = inputfiledir+'/药物_成份'
diseases = inputfiledir+'/药物_疾病'
avoids = inputfiledir+'/禁忌'
approval_nums = inputfiledir+'/批准文号'
dispensatories = inputfiledir+'/药品说明书'
drug_disp = inputfiledir+'/药物_说明书'

f1 = File.directory(drugs).delimiter('|').header('name','drug_category')
f2 = File.directory(manufacturers).delimiter('|').header('name')
f3 = File.directory(components).delimiter('|').header('aname','bname')
f4 = File.directory(diseases).delimiter('|').header('aname','bname')
f5 = File.directory(avoids).delimiter('|').header('aname','bname')
f6 = File.directory(approval_nums).delimiter('|').header('aname','bname', 'p_approval_number')
f7 = File.directory(dispensatories).delimiter('|').header("name", "p_approval_number", "p_component", "character", "indication", "p_manufacturer", "main_cure", "effect_type", "untoward_reaction", "taboo", "standard", "product_name", "usage", "notes", "torage", "drug_interactions", "pharmacology", "overdose", "warning", "for_olds", "for_children", "dosage_form", "validity", "specification", "for_pregnant", "revision_date", "pharmacokinetics", "packaging", "URL")
f8 = File.directory(drug_disp).delimiter('|').header('aname','bname')

// 药物节点信息
load(f1).asVertices {
    label "drug"
    key "name"
}

// 生产厂商
load(f2).asVertices {
    label "manufacturer"
    key "name"
}

// 说明书节点信息
load(f7).asVertices {
    label "dispensatory"
    key "name"
}

// 药物——成份
load(f3).asEdges {
    label "含有"
    outV "aname", {
        label "drug"
        key "name"
    }
    inV "bname", {
        label "component"
        key "name"
    }
}

// 药物——疾病
load(f4).asEdges {
    label "治疗"
    outV "aname", {
        label "drug"
        key "name"
    }
    inV "bname", {
        label "disease"
        key "name"
    }
}


// 药物——禁忌——药物
load(f5).asEdges {
    label "禁忌"
    outV "aname", {
        label "drug"
        key "name"
    }
    inV "bname", {
        label "drug"
        key "name"
    }
}

// 禁忌（反向）
load(f5).asEdges {
    label "禁忌"
    outV "bname", {
        label "drug"
        key "name"
    }
    inV "aname", {
        label "drug"
        key "name"
    }
}

// 药物——生产厂商——生产厂商
load(f6).asEdges {
    label "生产厂商"
    outV "aname", {
        label "drug"
        key "name"
    }
    inV "bname", {
        label "manufacturer"
        key "name"
    }
}

// 药物——说明书
load(f8).asEdges {
    label "说明书"
    outV "aname", {
        label "drug"
        key "name"
    }
    inV "bname", {
        label "dispensatory"
        key "name"
    }
}
