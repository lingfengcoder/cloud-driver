
<html>
<head>
  <!-- Import style -->
  <link
    rel="stylesheet"
    href="//cdn.jsdelivr.net/npm/element-plus/dist/index.css"
  />
  <!-- Import Vue 3 -->
  <script src="//cdn.jsdelivr.net/npm/vue@3"></script>
  <!-- Import component library -->
  <script src="//cdn.jsdelivr.net/npm/element-plus"></script>
</head>
<template>
  <div>
    <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
      <el-row>
        <el-form-item label="单行文本" prop="field104">
          <el-input v-model="formData.field104" placeholder="请输入单行文本" clearable :style="{width: '100%'}">
          </el-input>
        </el-form-item>
        <el-form-item label="单行文本" prop="field103">
          <el-input v-model="formData.field103" placeholder="请输入单行文本" clearable :style="{width: '100%'}">
          </el-input>
        </el-form-item>
        <el-form-item label="单行文本" prop="field102">
          <el-input v-model="formData.field102" placeholder="请输入单行文本" clearable :style="{width: '100%'}">
          </el-input>
        </el-form-item>
      </el-row>
      <el-form-item size="large">
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  components: {},
  props: [],
  data() {
    return {
      formData: {
        field104: undefined,
        field103: undefined,
        field102: undefined,
      },
      rules: {
        field104: [{
          required: true,
          message: '请输入单行文本',
          trigger: 'blur'
        }],
        field103: [{
          required: true,
          message: '请输入单行文本',
          trigger: 'blur'
        }],
        field102: [{
          required: true,
          message: '请输入单行文本',
          trigger: 'blur'
        }],
      },
    }
  },
  computed: {},
  watch: {},
  created() {},
  mounted() {},
  methods: {
    submitForm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        // TODO 提交表单
      })
    },
    resetForm() {
      this.$refs['elForm'].resetFields()
    },
  }
}

</script>
<style>
</style>
</html>

