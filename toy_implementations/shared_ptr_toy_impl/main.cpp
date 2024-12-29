#include <iostream>
#include <string>

#define CLASS_PRINT_FUNC_DEBUG \
    std::cerr << this << " | " << __PRETTY_FUNCTION__ << std::endl;

#define CLASS_LOG(...) \
    logMsg(this, __PRETTY_FUNCTION__, ##__VA_ARGS__);

template<typename... Args>
void logMsg(void* pObj, const char* fnName, Args... args)
{
    std::cout << pObj << " | " << fnName << " | ";
    int p[]{(std::cout << args, 0)...};
    std::cout << std::endl;
}

template<typename T>
struct MySharedPtr
{
    MySharedPtr() = default;

    template<typename... Args>
    MySharedPtr(Args... args)
        : m_pRefCount(new size_t(1))
        , m_pObj(new T(args...))
    {
        CLASS_PRINT_FUNC_DEBUG
    }

    ~MySharedPtr()
    {
        CLASS_PRINT_FUNC_DEBUG
        if (m_pObj != nullptr && m_pRefCount != nullptr)
        {
            if (--(*m_pRefCount) == 0)
            {
                CLASS_LOG("Last reference, freeing resource at ", m_pObj)
                delete m_pObj;
                delete m_pRefCount;
            }
        }
    }

    MySharedPtr(MySharedPtr const& e)
    {
        CLASS_PRINT_FUNC_DEBUG
        m_pObj      = e.m_pObj;
        m_pRefCount = e.m_pRefCount;
        (*m_pRefCount)++;
        CLASS_LOG("Reference count for resource at ", m_pObj, " is now ", *m_pRefCount)
    }

    MySharedPtr& operator=(MySharedPtr const& e)
    {
        CLASS_PRINT_FUNC_DEBUG

        // manage previous reference.
        if ( m_pObj != nullptr && m_pRefCount != nullptr)
        {
            if (--(*m_pRefCount) == 0)
            {
                CLASS_LOG("Previous reference is last reference, freeing resource at ", m_pObj)
                delete m_pObj;
                delete m_pRefCount;
            }
        }

        m_pObj      = e.m_pObj;
        m_pRefCount = e.m_pRefCount;
        (*m_pRefCount)++;

        CLASS_LOG("Reference count for resource at ", m_pObj, " is now ", *m_pRefCount)
        return *this;
    }

    MySharedPtr(MySharedPtr&& e)
    {
        CLASS_PRINT_FUNC_DEBUG
        m_pObj          = e.m_pObj;
        m_pRefCount     = e.m_pRefCount;
        e.m_pObj        = nullptr;
        e.m_pRefCount   = nullptr;
        CLASS_LOG("Reference count for resource at ", m_pObj, " is now ", *m_pRefCount)
    }

    MySharedPtr& operator=(MySharedPtr&& e)
    {
        CLASS_PRINT_FUNC_DEBUG

        // manage previous reference.
        if ( m_pObj != nullptr && m_pRefCount != nullptr)
        {
            if (--(*m_pRefCount) == 0)
            {
                CLASS_LOG("Previous reference is last reference, freeing resource at ", m_pObj)
                delete m_pObj;
                delete m_pRefCount;
            }
        }

        m_pObj          = e.m_pObj;
        m_pRefCount     = e.m_pRefCount;
        e.m_pObj        = nullptr;
        e.m_pRefCount   = nullptr;

        CLASS_LOG("Reference count for resource at ", m_pObj, " is now ", *m_pRefCount)
        return *this;
    }

    T* const get()
    {
        return m_pObj;
    };

private:
    T* m_pObj           = nullptr;
    size_t* m_pRefCount = nullptr;
};

struct MyTestClass
{
    MyTestClass(std::string const val)
        : m_value(val)
    {
        CLASS_PRINT_FUNC_DEBUG
    }

    ~MyTestClass()
    {
        CLASS_PRINT_FUNC_DEBUG
    }

    std::string const getValue()
    { 
        return m_value;
    }

private:
    std::string m_value;
};

int main()
{
    std::cout << "first pointer." << std::endl;
    MySharedPtr<MyTestClass> ptr;

    {
        std::cout << "Creating shared ptr of MyTestClass in scope" << std::endl;
        auto ptr2 = MySharedPtr<MyTestClass>("asdf");

        std::cout << "Moving to global ptr" << std::endl;
        ptr = std::move(ptr2);
    }

    {
        auto ptr2 = ptr;
        std::cout << "ptr2 copied from ptr with value: " << ptr2.get()->getValue() << std::endl;

        auto ptr3 = MySharedPtr<MyTestClass>("fdsa");
        std::cout << "ptr3 created with value: " << ptr3.get()->getValue() << std::endl;
        std::cout << "copy ptr -> ptr3 should result in destruction of resource at " << ptr3.get() << std::endl;
        ptr3 = ptr;
        std::cout << "now ptr3 have the value: " << ptr3.get()->getValue() << std::endl;
    }
}
